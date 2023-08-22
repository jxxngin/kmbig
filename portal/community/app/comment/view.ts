import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import toastr from 'toastr';

export class Component implements OnInit {
    private comment = [];
    private login = {};
    private post = { id: "", content: "" };
    private text = "";
    private debouncer = new Subject<string>();

    constructor(public service: Service) {
        this.debouncer.pipe(debounceTime(30)).subscribe(() => this.upload());
    }

    public async ngOnInit() {
        await this.service.init();
        this.load();
    }

    private async load() {
        this.post.id = WizRoute.segment.id;
        let { code, data } = await wiz.call('load', { board_id: this.post.id });

        const { comment, login } = data;
        this.comment = comment;
        this.login = login;

        await this.service.render();
    }

    private async onEnter() {
        this.debouncer.next();
    }

    private async upload() {
        if (this.text == "") {
            toastr.warning("내용을 입력해주세요");
            return;
        }

        this.post.content = this.text;
        let { code } = await wiz.call('upload', this.post);

        if (code != 200) {
            alert("잘못된 접근입니다.");
        }
        this.text = '';

        let el = document.getElementsByClassName('form-control');
        for(let i = 0; i < el.length; i++) {
            el[i].value = "";
        }

        await this.load();
    }

    private async del(id: number) {
        let res = await this.service.alert.show({
            title: "",
            message: "정말 이 댓글을 삭제하겠습니까?",
        });

        if (!res)
            return;

        let { code, data } = await wiz.call('delete', { id });
        await this.load();
    }

    private async update(id: number, text: string) {
        let { code, data } = await wiz.call('update', { id, text })
        await this.load();
    }
}