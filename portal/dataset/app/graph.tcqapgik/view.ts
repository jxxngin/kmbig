import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.loadFile();
        await this.loadGraph();
    }

    public async loadFile() {
        this.dataset_id = WizRoute.segment.id;
        let { code, data } = await wiz.call("fileInfo", {"id":this.dataset_id});
        await this.service.render();
    }

    public async loadGraph() {
        const data = {
            labels: [],
            datasets: [{
                label: "라벨 이름",
                data: [],
                backgroundColor: [],
                borderColor: [],
                borderWidth: 1,
            }]
        };

        const config = {
            type: '그래프 유형',
            data: data,
            options: {
            },
        };

        const ctx = document.getElementById('widget-graph').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}