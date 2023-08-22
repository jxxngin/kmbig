import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    @Input() list: any;
    @Input() mode: any;


    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.loading(true);
        await this.file_load();
        await this.loading(false);
    }

    public async file_load() {
        this.dataset_id = WizRoute.segment.id;
        this.category = WizRoute.segment.category;
        let { code, data } = await wiz.call("file_info", { "id": this.dataset_id, "category": this.category });
        this.file = data;
        // this.file = data.df;
        // this.filename = data.filename;
        // this.filepath = data.filepath;
        // this.file_rows = data.file_row;

        this.columns = [];
        for (let value of this.file) {
            for (let key in value) {
                if (!this.columns.includes(key)) {
                    this.columns.push(key);
                }
            }
        }
        await this.service.render();
    }

    public tab(mode) {
        this.mode = mode;
        this.service.render();
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}
