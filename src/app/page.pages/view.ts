import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { ActivatedRoute } from '@angular/router';

export class Component implements OnInit {
    private _loading = false;

    constructor(
        public service: Service,
        public route: ActivatedRoute,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.loading(true);
        this.route.url.subscribe(([_, { path }]) => {
            // console.log('url : ', path)
            this.pages(path);
        })
        // await this.loading(false);
    }

    public async pages(path) {
        // console.log('route : ', WizRoute.segment)
        // this.page = WizRoute.segment.category;
        let { code, data } = await wiz.call('pages', { 'page': path });
        this.html = data.content;
        await this.loading(false);
        // await this.service.render();
    }

    private async loading(act) {
        this._loading = act;
        await this.service.render();
    }
}