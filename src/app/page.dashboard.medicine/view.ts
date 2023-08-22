import { Service } from '@wiz/libs/portal/season/service';
import { Router, Event, NavigationEnd } from '@angular/router';

export class Component implements OnInit {

    public categoryLs = {
        id: "",
        title: "",
        category: "",
        content: ""
    }
    public datasetLs = []
    public datasetID: any;
    public fileInfo: any;

    constructor(
        public service: Service,
        public router: Router
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.load();
        await this.service.render();
    }

    public async load() {
        this.datasetID = this.router.url.split('/')[2];
        let { code, data } = await wiz.call("load", { "id": "한약재" });
        this.datasetLs = data.dataset_row;
        this.categoryLs = data.dashboard_row;
        this.fileInfo = data.fileInfo;
        await this.service.render();
    }

    public async download(file) {
        let download = wiz.url('download?file=' + file)
        window.location.href = download;
    }
}