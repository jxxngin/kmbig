import { OnInit } from '@angular/core';

export class Component implements OnInit {
    public menu_ls = [
        { url: "/page/intro", name: "KMBIG 소개", index: "page" },
        { url: "/dashboard/device", name: "데이터셋 대시보드", index: "dashboard" },
        { url: "/share/user/form", name: "데이터셋 공유", index: "share" },
        { url: "/dataset/search", name: "데이터셋 검색", index: "search" },
        { url: "/survey/ocr", name: "설문", index: "survey" },
        { url: "/community/notice/list", name: "커뮤니티", index: "community" }
    ];
    private current = "";

    constructor() { }

    public async ngOnInit() {
    }

    private async log(item) {
        console.log(item);
    }
}