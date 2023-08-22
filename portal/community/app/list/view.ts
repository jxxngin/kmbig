import { OnInit } from '@angular/core';
import { Router, ActivatedRoute, Event, NavigationEnd } from '@angular/router';
import { Service } from '@wiz/libs/portal/season/service';
import toastr from 'toastr';

export class Component implements OnInit {
    private list = [];
    private search_word = "";
    private login;
    private category = "";
    private _loading = false;

    private page = {
        current: 1,
        start: 1,
        end: 1,
    };

    constructor(
        public service: Service,
        private router: Router,
        public route: ActivatedRoute,
    ) { }

    public async ngOnInit() {
        await this.service.init();

        this.category = WizRoute.segment.category;
        await this.load();

        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                this.category = WizRoute.segment.category;
                await this.move(1);
            }
        })
    }

    private async load() {
        if (this.category === undefined) {
            return;
        }

        await this.loading(true);
        let { code, data } = await wiz.call('load', { page: this.page.current, category: this.category });
        const { list, lastpage, login } = data;

        this.page.start = (parseInt(this.page.current / 11) * 10) + 1;
        this.page.end = lastpage;
        this.list = list;
        this.login = login;

        await this.loading(false);
        await this.service.render();
    }

    private async search(data: string) {
        toastr.success('Search: ' + data);
    }

    private async move(index: number) {
        this.page.current = index;
        await this.load();
    }

    private async show(id) {
        if (this.login) {
            this.service.href('/community/' + this.category + '/view/' + id);
        }
        else {
            alert('로그인 후 이용가능한 서비스 입니다');
        }
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}