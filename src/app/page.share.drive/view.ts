import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

import { FlatTreeControl } from '@angular/cdk/tree';
import { FileNode, FileDataSource } from '@wiz/libs/drive/file';

@dependencies({
    MatTreeModule: '@angular/material/tree'
})

export class Component implements OnInit {
    private storage = null;
    private root = null;
    private base = null;
    private path = null;

    public rootNode: FileNode;
    private treeControl: FlatTreeControl<FileNode>;
    private dataSource: FileDataSource;
    private getLevel = (node: FileNode) => node.level;
    private isExpandable = (node: FileNode) => node.extended;

    private mkdir = false;
    private dirName = "";

    private selectAll = false;
    private isRenaming = {};


    public macroTF = false;
    public fileSelect = [];
    public selected = "none";
    public macroFilepath: any;

    constructor(
        public service: Service
    ) {
        this.rootNode = new FileNode('root', this.root, 'folder');
        this.treeControl = new FlatTreeControl<FileNode>(this.getLevel, this.isExpandable);
        this.dataSource = new FileDataSource(this);
    }

    public async ngOnInit() {
        await this.service.init();

        this.rootNode = new FileNode('root', this.root, 'folder');
        this.treeControl = new FlatTreeControl<FileNode>(this.getLevel, this.isExpandable);
        this.dataSource = new FileDataSource(this);

        await this.init();
    }

    private async init() {
        let { code, data } = await wiz.call("init");
        if (code !== 200) {
            alert("오류가 발생했습니다. 다시 시도해주세요.");
            location.reload();
        }
        this.root = data;
        this.base = data;

        let res = await this.list(this.rootNode);
        this.dataSource.data = res;

        await this.load();
    }

    public async load() {
        let { code, data } = await wiz.call("load", { base: this.base });
        this.user = data.user;
        this.files = data.files.filter(file => !(file.name === "cache" && file.type === "folder"));

        this.dirName = "";
        this.path = this.base.replace(this.root, '');
        this.mkdir = false;
        this.selectAll = false;

        await this.service.render();
    }

    private async list(node: FileNode) {
        let { code, data } = await wiz.call("list", { path: this.base });
        data = data.map(item => new FileNode(item.name, item.path, item.type, node, node.level + 1));
        // data.sort((a, b) => {
        //     if (a.type == b.type)
        //         return a.path.localeCompare(b.path);
        //     if (a.type == 'folder') return -1;
        //     if (b.type == 'folder') return 1;
        // });
        return data;
    }

    private async move(node: FileNode) {
        if (node === undefined) {
            await this.init();
            return;
        }

        if (node.type === "folder") {
            this.base = node.path;
        }

        for (let i = 0; i < this.dataSource.data.length; i++) {
            this.dataSource.data[i].active = false;
        }

        if (node.extended == true) {
            node.parent.active = true;
            await this.dataSource.toggle(node, false);
            this.base = this.base.substring(0, this.base.lastIndexOf('/'));
            await this.load();
            return;
        }

        node.active = true;

        await this.dataSource.toggle(node, true);
        await this.load();
    }

    private async remove() {
        let alert = await this.service.alert.show({
            title: "",
            message: "정말 이 파일을 삭제하겠습니까?",
            cancel: "No",
        });

        if (!alert) {
            return;
        }

        for (let file of this.files) {
            if (file.checked) {
                let { code, data } = await wiz.call("remove", { base: this.base, file: JSON.stringify(file) });
                if (code !== 200) {
                    alert("remove 과정에서 오류가 발생했습니다.");
                    return;
                }
            }
        }
        let res = this.dataSource.data.find(item => item.path === this.base);
        await this.refresh(res);

        await this.load();
    }

    private async create() {
        if (!this.mkdir) {
            this.mkdir = true;
            setTimeout(async () => {
                const inputEl = document.querySelector("#mkdir");
                inputEl.focus();
            }, 300);
        }
        else {
            if (this.dirName.length === 0) {
                return;
            }

            let { code, data } = await wiz.call("create", { base: this.base, dirName: this.dirName });
            if (code !== 200 && code !== 201) {
                this.mkdir = false;
                alert("create 과정에서 오류가 발생했습니다.");
                return;
            }
            else if (code === 201) {
                this.service.toast.error("이미 존재하는 이름입니다.");

                setTimeout(async () => {
                    const inputEl = document.querySelector("#mkdir");
                    inputEl.focus();
                }, 300);

                return;
            }
            this.mkdir = false;

            let res = this.dataSource.data.find(item => item.path === this.base);
            await this.refresh(res);

            await this.load();
        }
        await this.service.render();
    }

    private async upload(data = null) {
        let files = data;
        if (files == null) {
            files = await this.service.file.select({ accept: '.xls,.xlsx,.csv', multiple: true });
        }

        let fd = new FormData();
        let filepath = [];

        for (let i = 0; i < files.length; i++) {
            if (!files[i].filepath) files[i].filepath = this.base;
            else {
                let to = files[i].filepath.substring(0, files[i].filepath.lastIndexOf('/'));
                files[i].filepath = this.base + "/" + to;
            }
            fd.append('file[]', files[i]);
            filepath.push(files[i].filepath);
        }

        fd.append("filepath", JSON.stringify(filepath));

        let url = wiz.url('upload');
        await this.service.file.upload(url, fd);

        let res = this.dataSource.data.find(item => item.path === this.base);
        await this.refresh(res);

        await this.load();
    }

    private async drop($event) {
        $event.preventDefault();
        let files = await this.service.file.drop($event);

        await this.upload(files);
    }

    private async checkAll() {
        for (const file of this.files) {
            file.checked = this.selectAll;
        }
    }

    private async checked(file) {
        file.checked = !file.checked;
        this.selectAll = this.files.every(file => file.checked);

        // macro
        this.macroTF = false;
        if (file.checked == true) {
            this.fileSelect.push(file);
        } else {
            let copy = this.fileSelect;
            this.fileSelect = copy.filter((element) => element !== file);
        }
        if (this.fileSelect.length == 1 && this.fileSelect[0].type == "file") {
            let { code, data } = await wiz.call("macro", {"filepath":file.path});
            if (code != 200) return;
            this.macro = data;
            this.macroTF = true;
        }
        
        await this.service.render();
    }

    public close() {
        this.macroTF = false;
        this.selected = "none";
        this.fileSelect[0].checked = false;
        this.fileSelect = [];
        this.service.render();
        this.load();
    }

    public async macroSelect(selected) {
        this.macroFilepath = this.fileSelect[0].path;
        this.selected = selected;
        await this.service.render();
    }

    private async goBack() {
        let oldPath = this.base;
        this.base = this.base.substring(0, this.base.lastIndexOf('/'));

        let res = this.dataSource.data.find(item => item.path === oldPath);
        await this.move(res);
    }

    private async open(file) {
        let filePath = file.path.split(this.root);
        file.path = this.root + filePath.slice(1).join(this.root);

        let res = this.dataSource.data.find(item => item.name === file.name && item.path === file.path);
        if (res) {
            await this.move(res);
        }
    }

    private async rename(file, i) {
        if (!this.isRenaming[i]) {
            this.isRenaming[i] = true;
            setTimeout(async () => {
                const inputEl = document.querySelector("#rename");
                inputEl.focus();
            }, 300);
        }
        else {
            if (file.name.length === 0) {
                this.service.toast.error("이름은 비워둘 수 없습니다");
                return;
            }

            let filter = this.files.filter(item => item.name === file.name);

            let { code } = await wiz.call("rename", { base: this.base, name: file.name, path: file.path });
            if (code === 200) {
                this.isRenaming[i] = false;

                let filePath = file.path.split(this.root);
                file.path = this.root + filePath.slice(1).join(this.root);

                let res = this.dataSource.data.find(item => item.path === this.base);
                await this.refresh(res);

                await this.load();
            }
            else if (code === 201) {
                this.isRenaming[i] = false;
                this.service.toast.error("존재하지 않는 파일입니다.");
                return;
            }
            else if (code === 202) {
                this.service.toast.error("이미 존재하는 이름입니다.");

                setTimeout(async () => {
                    const inputEl = document.querySelector("#rename");
                    inputEl.focus();
                }, 300);

                return;
            }
            else {
                this.isRenaming[i] = false;
                alert("rename 과정에서 오류가 발생했습니다.");
                return;
            }
        }
        await this.service.render();
    }

    public async download(file) {
        let download = wiz.url("download?path=" + this.base + "&name=" + file.name)
        window.open(download, '_blank');
    }

    public async refresh(node: FileNode | null = null) {
        if (node && node.parent) {
            await this.dataSource.toggle(node, false);
            await this.dataSource.toggle(node, true);
        } else {
            let data = await this.list(this.rootNode);
            this.dataSource.data = data;
        }
    }

    public filesize(value) {
        if (!value) return "--";
        let kb = value / 1024;
        if (kb < 1) return value + "B";
        let mb = kb / 1024;
        if (mb < 1) return Math.round(kb * 100) / 100 + "KB";
        let gb = mb / 1024;
        if (gb < 1) return Math.round(mb * 100) / 100 + "MB";
        return Math.round(gb * 100) / 100 + "GB";
    }
}