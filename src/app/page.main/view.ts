import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private info = [];

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        const { code, data } = await wiz.call("load_card");
        if (code == 200) {
            this.info = data;
        }
    }
}