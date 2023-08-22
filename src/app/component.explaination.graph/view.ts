import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Input() title: any;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
    }
}