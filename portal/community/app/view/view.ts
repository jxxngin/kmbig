import { OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private view = {};
    private login = {};
    private user = {};
    private category = "";
    private post_id;

    constructor(
        public service: Service,
        private router: Router,
        private route: ActivatedRoute,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    private async load() {
        this.post_id = WizRoute.segment.id;
        this.category = WizRoute.segment.category;

        if (this.post_id == 'new') {
            alert('잘못된 접근입니다.');
            this.service.href(['/community/list']);
        }

        let { code, data } = await wiz.call('load', { id: this.post_id });
        if (code != 200) {
            alert('Error!');
        }
        const { view, user, login } = data;
        this.view = view;
        this.user = user;
        this.login = login;

        await this.service.render();
    }
}