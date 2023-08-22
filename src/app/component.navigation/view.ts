import { Input, OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { ActivatedRoute, Router, Event, NavigationStart, NavigationEnd, NavigationError } from '@angular/router';

export class Component implements OnInit {
    @Input() title = "한국한의학연구원";

    public isMenuCollapsed: boolean = true;
    public isDesktop: boolean;
    public userRole = "none";

    private showNoti = false;
    private newNoti = false;

    public menu_ls = [
        { url: "/page/intro", name: "KMBIG 소개", index: "page" },
        { url: "/dashboard/device", name: "데이터셋 대시보드", index: "dashboard" },
        { url: "/share/user/form", name: "데이터셋 공유", index: "share" },
        { url: "/dataset/search", name: "데이터셋 검색", index: "search" },
        // { url: "/survey", name: "설문", index: "survey" },
        { url: "/survey/result/hnynpq1ttyijjdp3", name: "설문", index: "survey" },
        { url: "/community/notice/list", name: "커뮤니티", index: "community" }];

    public dashboard_ls = [];
    constructor(
        public service: Service,
        public route: ActivatedRoute,
        public router: Router,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        if (Object.keys(this.service.auth.session).length === 0) {
            this.menu_ls.splice(2, 1); // 데이터셋 공유
            this.menu_ls.splice(3, 1); // 설문
        } else {
            this.userRole = "user";
            if (this.service.auth.session.role === "admin") {
                this.userRole = "admin";
                this.menu_ls[4].url = "/survey";
                await this.service.render();
            }
        }
        this.currentRoute = this.router.url;
        await this.load();
        this.router.events.subscribe((event: Event) => {
            if (event instanceof NavigationEnd) {
                // this.currentRoute = event.url;
                // this.service.render();
            }
            this.display(false);
            // this.load();

        })
        await this.service.render();
    }

    public async load() {
        let { code, data } = await wiz.call("load");
        if (code != 200) return;
        this.dash = data;
        for (let item of this.dash) {
            this.dashboard_ls.push({ url: `/dashboard/${item.category}`, name: `${item.title} 데이터셋` })
        }
        this.username = this.service.auth.session.name;
        this.userrole = this.service.auth.session.role;
        if (this.userrole == 'admin') {
            this.menu_ls[0].url = "/page/edit/intro"
        }
        await this.notify();
        await this.service.render();
    }

    public async collapse() {
        this.isMenuCollapsed = !this.isMenuCollapsed;
        await this.service.render();
    }

    private highlight(index) {
        this.currentRoute = this.router.url;
        this.contain = this.currentRoute.indexOf(index);

        if (this.contain == -1) return false;
        else return true;
    }

    public menuActive(url: string) {
        let path = location.pathname;
        if (path.indexOf(url) == 0) return 'active';
        return '';
    }

    private async display(opt = null) {
        if (opt === null) {
            this.showNoti = !this.showNoti;
        }
        else {
            this.showNoti = opt;
        }
        await this.service.render();
    }

    private async notify() {
        const { code, data } = await wiz.call("noti");
        this.newNoti = data;
        await this.service.render();
    }
}