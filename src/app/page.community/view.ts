import { OnInit } from '@angular/core';
import { Router, ActivatedRoute, Event, NavigationEnd } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private mode = 'list';

    constructor(
        public service: Service,
        private router: Router,
        private route: ActivatedRoute,
    ) { }

    public async ngOnInit() {
        await this.service.init();

        await this.setting();

        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                await this.setting();
            }
        })
    }

    private async setting() {
        this.mode = WizRoute.segment.mode;
        await this.service.render();
    }
}