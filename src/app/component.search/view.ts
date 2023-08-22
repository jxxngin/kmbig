import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    private searchText = "";
    private list = [];
    private tags = [];
    private filtered = [];
    private currentIndex = null;

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.getList();
        await this.getTag();
    }

    private async alert(message: string, status: string = 'error') {
        return await this.service.alert.show({
            title: "",
            message: message,
            cancel: false,
            actionBtn: status,
            action: "확인",
            status: status
        });
    }

    private async getList() {
        let { code, data } = await wiz.call("wrap");
        if (code !== 200) {
            let msg = "검색바를 불러오는 과정에서 오류가 발생했습니다.";
            await this.alert(msg);
            return;
        }
        this.list = data;
        this.filtered = data.slice(0, 10);
        await this.service.render();
    }

    private async getTag() {
        const { code, data } = await wiz.call("tag");
        if (code !== 200) {
            let msg = "추천 검색어를 불러오는 과정에서 오류가 발생했습니다.";
            await this.alert(msg);
            return;
        }
        
        let indices = Array.from({length: data.length}, (_, i) => i);
        indices = this.shuffle(indices);

        const cnt = 4;
        for (let i = 0; i < cnt; i++) {
            this.tags.push(data[indices[i]]);
        }

        await this.service.render();
    }

    private shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }

    private async onSearch() {
        const { code } = await wiz.call("log", { text: this.searchText });
        if (code !== 200) {
            let msg = "검색 과정에서 오류 발생!";
            await this.alert(msg);
            return;
        }

        let url = "/dataset/search";
        if (this.searchText)
            url += "?text=" + this.searchText;
        this.onBlur();
        this.service.href(url);
    }

    private async doSearch() {
        if (this.searchText) {
            this.filtered = this.list.filter((item) => item.includes(this.searchText));
            this.filtered = this.filtered.slice(0, 10);
            await this.service.render();
        }
    }

    private async onKeyDown(event: KeyboardEvent) {
        let key = event.key;
        let len = this.filtered.length;

        switch (key) {
            case "ArrowDown":
                if (this.currentIndex === null) {
                    this.currentIndex = 0;
                }
                else {
                    if (this.currentIndex === len - 1) {
                        this.currentIndex === null;
                    }
                    else {
                        this.currentIndex = (this.currentIndex + len + 1) % len;
                    }
                }
                break;

            case "ArrowUp":
                if (this.currentIndex === null) {
                    this.currentIndex = len - 1;
                }
                else {
                    if (this.currentIndex === 0) {
                        this.currentIndex = null;
                    }
                    else {
                        this.currentIndex = (this.currentIndex + len - 1) % len;
                    }
                }
                break;

            case "Escape":
                document.activeElement.blur();
                return;

            case "Enter":
                if (event.isComposing)
                    return;
                if (this.currentIndex != null)
                    this.searchText = this.filtered[this.currentIndex];
                this.currentIndex === null;
                await this.onSearch();
                break;

            default:
                return;
        }

        let target = document.querySelectorAll(".autocomplete-item")[this.currentIndex];
        if (target && target.scrollIntoView) {
            target.scrollIntoView(false);
        }
        await this.service.render();
    }

    private async onClick(idx) {
        this.searchText = this.filtered[idx];
        await this.onSearch();
    }

    private async recommend(tag) {
        this.searchText = tag;
        await this.onSearch();
    }

    private async currentSearch(idx) {
        this.currentIndex = idx;
        await this.service.render();
    }

    private async onBlur() {
        const element = document.querySelector('.form-control') as HTMLElemnt;
        element.blur();
    }
}