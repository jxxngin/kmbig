import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        let session = this.service.auth.session;
        if (Object.keys(session).length === 0) {
            this.service.href(`/`);
            return;
        }
        this.userRole = session.role;

        await this.load();
        await this.service.render();
    }

    public async load() {
        let { code, data } = await wiz.call("load");
        if (code == 200) {
            this.list = data;
        }
    }

    public async edit(id) {
        location.href = `/ocr/edit/${id}`;
    }
}