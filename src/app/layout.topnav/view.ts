import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Router } from '@angular/router';

export class Component implements OnInit {
    constructor(
        public service: Service,
        public router: Router
    ) { }

    public isDesktop: boolean;

    public async ngOnInit() {
        await this.service.init();
        this.isDesktop = window.innerWidth >= 768;
        this.currentRoute = this.router.url;
    }
}