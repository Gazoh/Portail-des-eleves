import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ApiService} from "../../api.service";

@Component({
  selector: 'repartitions-sidebar',
  templateUrl: './repartitions-sidebar.component.html',
  styleUrls: ['./repartitions-sidebar.component.scss']
})

export class RepartitionsSidebarComponent implements OnInit {

    @Input() campagnes: any;
    @Input() displayParameters: any;

    @Output() onNewRequested = new EventEmitter();

    constructor(private apiService: ApiService) { }

    ngOnInit() {
    
    }

    requestNew()
    {
    	this.onNewRequested.emit();
    }

}