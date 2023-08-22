import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import toastr from 'toastr';

export class Component implements OnInit {
    private post = {};
    private login = {};
    private category = "";

    private status = {
        upload: false,
        upload_process: '0',
    };

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
    }

    private async load() {
        this.post.id = WizRoute.segment.id;
        this.category = WizRoute.segment.category;
        if (this.post.id !== 'new') {
            let { code, data } = await wiz.call('load', { id: this.post.id })
            if (code !== 200) {
                alert('ERROR')
            }
            const { post, login } = data;
            this.post = post;
            this.login = login;
            await this.service.render();
        }
    }

    private async update() {
        if (WizRoute.segment.id !== 'new') {
            let { code, data } = await wiz.call('update', this.post);
        }
        else {
            this.post.category = this.category;
            let { code, data } = await wiz.call('create', this.post);
        }

        this.service.href('/community/'+this.category+'/list');
    }

    private async del() {
        let res = await this.service.alert.show({
            title: "게시글 삭제",
            message: "정말로 이 게시글을 삭제하겠습니까?",
        });

        if (!res)
            return;

        let { code } = await wiz.call('delete', { id: this.post.id });
        if (code == 200) {
            this.service.href('/community/'+this.category+'/list');
        }
        else {
            alert('ERROR!');
        }
    }

    // File 관련 기능
    private async upload() {
        toastr.error('아직 지원하지 않는 기능입니다');
    }

    private async delete_file(item) {
        toastr.error('아직 지원하지 않는 기능입니다');
    }
}