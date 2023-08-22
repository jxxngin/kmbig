import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { ActivatedRoute, Router, Event, NavigationStart, NavigationEnd, NavigationError } from '@angular/router';

export class Component implements OnInit {

    public pages_ls = [
        { url: "/page/intro", name: "KMBIG 소개" },
        { url: "/page/help", name: "이용안내" },
        { url: "/page/term", name: "이용약관" },
        { url: "/page/privacy", name: "개인정보처리방침" },
        { url: "/page/service", name: "연계서비스" },
        { url: "/page/request", name: "제공신청안내" }];

    public pages_edit_ls = [
        { url: "/page/edit/intro", name: "KMBIG 소개" },
        { url: "/page/edit/help", name: "이용안내" },
        { url: "/page/edit/term", name: "이용약관" },
        { url: "/page/edit/privacy", name: "개인정보처리방침" },
        { url: "/page/edit/service", name: "연계서비스" },
        { url: "/page/edit/request", name: "제공신청안내" }];

    public dashboard_ls = [
        { url: "/dashboard/device", name: "기기 데이터셋" },
        { url: "/dashboard/medicine", name: "한약재 데이터셋" },
        { url: "/dashboard/multiple", name: "응용 데이터셋" }];
    // public dashboard_ls = [
    //     { url: "/dashboard/device", name: "기기 데이터셋" }
    // ];
    // public dashboard_ls = [];

    public share_ls = [
        { url: "/share/user/form", name: "내 공유요청 목록" },
        { url: "/share/expert/form", name: "전문가 공유심사" },
        { url: "/share/drive", name: "연구자 서랍" }];

    // public survey_ls = [
    //     { url: "/survey/ocr", name: "OCR" },
    //     { url: "/survey", name: "설문 분석" }];

    public community_ls = [
        { url: "/community/notice/list", name: "공지사항" },
        { url: "/community/qna/list", name: "문의게시판" }];

    constructor(
        public service: Service,
        public route: ActivatedRoute,
        public router: Router,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        if (Object.keys(this.service.auth.session).length === 0 || this.service.auth.session.is_expert == 0) {
            this.share_ls.splice(1, 1);
        }
        this.currentRoute = this.router.url;
        this.menu = this.currentRoute.split("/")[1];

        this.router.events.subscribe(async (event: Event) => {
            if (event instanceof NavigationEnd) {
                this.currentRoute = event.url;
                this.menu = this.currentRoute.split("/")[1];
                await this.service.render();
            }
            // this.load();
        })
        await this.load();
        await this.service.render();
    }

    public async load() {
        let { code, data } = await wiz.call("load");
        if (code != 200) return;
        this.dash = data;
        // for(let item of this.dash) {
        //     this.dashboard_ls.push({url:`/dashboard/${item.category}`, name: `${item.title} 데이터셋`})
        // }

        this.username = this.service.auth.session.name;
        this.userrole = this.service.auth.session.role;
        if (this.userrole == 'admin') {
            this.pages_ls = this.pages_edit_ls;
        }
        await this.service.render();
    }
}

