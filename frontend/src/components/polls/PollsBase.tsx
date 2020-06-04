import React from "react";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { PollsSidebar } from "./PollsSidebar";
import Container from "react-bootstrap/Container";
import { authService } from "../../App";
import { Link } from "react-router-dom";

export const PollsBase = ({
    children,
    sidebarActions,
}: {
    children: any;
    sidebarActions?: any;
}) => (
    <Container className="mt-5">
        <Link to="/" className="display-4">
            Lien vers l’accueil
        </Link>
        <br />
        <Link to="/trombi" className="display-4">
            Lien vers le trombi
        </Link>
        <br />
        <Link to="/associations/" className="display-4">
            Lien vers les associations
        </Link>
        <br />
        <Link to="/sondages" className="display-4">
            Lien vers les sondages
        </Link>
        <br />

        <Row>
            <Col md="3">
                <PollsSidebar
                    isStaff={authService.isStaff}
                    actions={sidebarActions}
                />
            </Col>
            <Col md="9">{children}</Col>
        </Row>
    </Container>
);
