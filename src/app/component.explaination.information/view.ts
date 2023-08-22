import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Input() list: any;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.file_load();
    }

    public async file_load() {
        this.dataset_id = WizRoute.segment.id;
        this.category = WizRoute.segment.category;

        let { code, data } = await wiz.call("file_info", { "id": this.dataset_id, "category": this.category });
        this.file_rows = data.rows;
        await this.service.render();
    }
}