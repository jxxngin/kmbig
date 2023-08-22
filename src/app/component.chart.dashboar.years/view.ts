import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    @Input() title: any;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        await this.loadFile();
    }

    public async loadFile() {
        let { code, data } = await wiz.call("load");
        this.labels = data.labels;
        this.datas = data.datas;
        this.colors = ['#5041F2', '#F2748D', '#9996B7'];
        await this.service.render();
        await this.loadGraph();
    }

    public async loadGraph() {
        const data = {
            labels: this.labels,
            datasets: [{
                label: '데이터 건수',
                data: this.datas,
                backgroundColor: this.colors,
                borderColor: this.colors,
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
                        // display:false,
                        position: 'bottom',
                        labels: {
                            // pointStyle: "circle"
                            usePointStyle: true,
                        }
                    },
                }
            },
        };

        const actions = [
            {
                name: 'Toggle Point Style',
                handler(myChart) {
                    myChart.options.plugins.legend.labels.usePointStyle = !myChart.options.plugins.legend.labels.usePointStyle;
                    myChart.update();
                }
            },
        ];

        const ctx = document.getElementById('widget-years').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}