import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        let session = this.service.auth.session;
        console.log("session : ", session)
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

    public async add() {
        await this.service.href(`/survey/edit/new`);
    }

    public async edit(id) {
        await this.service.href(`/survey/edit/${id}`);
    }

    public async result(id) {
        await this.service.href(`/survey/result/${id}`);
    }
}