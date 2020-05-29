import {Component} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import {BaseMarketplaceComponent} from "../base-marketplace-component";
import {ApiService} from "../../api.service";
import { BasketManagerService } from "../basket-manager.service";
import { BasketItem, Marketplace, Product, RawMarketplace, RawProduct } from '../models';

@Component({
    selector: 'app-marketplace-counter',
    templateUrl: './marketplace-manager-counter.component.html',
    styleUrls: ['./marketplace-manager-counter.component.scss']
})
export class MarketplaceManagerCounterComponent extends BaseMarketplaceComponent {

    users$: any;
    products$: Observable<Product[]>;
    balance: number;

    userSearch = "" ;
    productSearch = "" ;

    buyer: any;
    userBasket: { [id: number] : BasketItem } = {} ;
    numberOfBuyerItems = 0 ;

    moneyToAdd: any ;
    addMoneyMessage = "";
    addMoneyStatus = "" ;

    constructor(api: ApiService, route: ActivatedRoute, manager: BasketManagerService) {
        super(api, route, manager);
    }

    ngOnInit() {
        this.route.params.subscribe(params => {
            const id = params['id'];

            this.api.get<RawMarketplace>(`marketplace/${id}/`).subscribe(
                rawMarketplace => {
                    this.marketplace = new Marketplace(rawMarketplace);
                    this.countItems();
                    this.updateProductSearch();
                },
                error => this.error = error.message
            );
        });

        this.updateUserSearch();
    }

    updateUserSearch(): void {
        this.users$ = this.api.get(`users/?search=${this.userSearch}`)
    }

    updateProductSearch(): void {
        const getProductsFromRaw = map((rawProducts: RawProduct[]) => rawProducts.map(rawProduct => new Product(rawProduct)));
        this.products$ = this.api.get<RawProduct[]>(`products/?marketplace=${this.marketplace.id}&search=${this.productSearch}`)
            .pipe(getProductsFromRaw);
    }

    setBuyer(user): void {
        this.buyer = user ;
        this.api.get(`marketplace/${this.marketplace.id}/balance/${this.buyer.id}`).subscribe(
            // @ts-ignore
            res => this.balance = res.balance
        )
    }

    getQuantity(product: Product): number {
        if (this.userBasket[product.id] == undefined) {
            return 0 ;
        } else {
            return this.userBasket[product.id].quantity;
        }
    }

    setQuantity(product: Product, value: number): void {
        this.userBasket[product.id].quantity = value;

        if (this.userBasket[product.id].quantity == 0) {
            delete this.userBasket[product.id];
        }

        this.countBuyerItems();
    }

    countBuyerItems(): void {
        this.numberOfBuyerItems = this.marketplace.products.reduce((acc: number, product: Product) => acc + this.getQuantity(product), 0);
    }

    addProduct(product: Product): void {
        if (this.userBasket[product.id] == undefined){
            this.userBasket[product.id] = new BasketItem(product, 1);
        } else {
            this.userBasket[product.id].quantity += 1;
        }

        this.countBuyerItems();
    }

    remove(product: Product): void {
        if(this.userBasket[product.id] != undefined && this.userBasket[product.id].quantity > 0){
            this.userBasket[product.id].quantity -= 1 ;
        }

        if(this.userBasket[product.id].quantity == 0){
            delete this.userBasket[product.id];
        }

        this.countBuyerItems();
    }

    order(): void {
        let basket = [] ;
        for (let id in this.userBasket) {
            basket.push({ id: id, quantity: this.userBasket[id].quantity });
        }

        this.api.post("orders/", {
            products: basket,
            user: this.buyer.id
        }).subscribe(
            res => {
                this.userBasket = {} ;
                this.buyer = null ;
                this.countItems();
            },
            err => {this.error = err.message ; }
        )
    }

    addMoney(): void {
        this.api.put(`marketplace/${this.marketplace.id}/balance/${this.buyer.id}`, {
            amount: parseFloat(this.moneyToAdd),
        }).subscribe(
            res => {
                this.addMoneyMessage = `${this.moneyToAdd}€ ajoutés`;
                this.addMoneyStatus  = "success" ;
                this.moneyToAdd = "" ;

                //setTimeout(_ => this.addMoneyMessage = "", 3000);
            },
            err => {
                this.addMoneyMessage = err.message;
                this.addMoneyStatus  = "error" ;
            }
        )
    }
}