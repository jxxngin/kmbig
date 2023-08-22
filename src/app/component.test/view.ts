import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';
import { OnInit } from '@angular/core';

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
        let { code, data } = await wiz.call("fileInfo", { "id": this.dataset_id });
        this.labels = data.labels;
        this.means = data.means;
        await this.service.render();
    }

    public async loadGraph() {
        const data = {
            labels: this.labels,
            datasets: [{
                label: "체온",
                data: this.means,
                backgroundColor: ["#FFEBEE", "#EF9A9A", "#EF5350"],
                borderColor: ["#FFEBEE", "#EF9A9A", "#EF5350"],
                borderWidth: 1,
                pointStyle: 'circle'
            }]
        };

        const config = {
            type: 'pie',
            data: data,
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                        }
                    },
                }
            },
        };

        const ctx = document.getElementById('widget-graph').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}