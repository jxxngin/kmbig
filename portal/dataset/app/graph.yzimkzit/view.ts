import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';

Chart.register(ChartDataLabels);

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
        if (!this.dataset_id) {
            this.dataset_id = "Giesy5Us4z6EekMlx12HcAfalV1JYasA";
        }
        let { code, data } = await wiz.call("fileInfo", { "id": this.dataset_id });
        this.labels = data.label;
        this.datas = data.value;
        this.colors = ['#F8F6D2', '#FFFBBA', '#FFF772', '#FEF428', '#FFED5C', '#FEEA2F', '#D6B866', '#8A7934'];
        await this.service.render();
    }

    public async loadGraph() {
        const total = this.datas.reduce((a, b) => a + b, 0);

        const data = {
            labels: this.labels,
            datasets: [{
                label: '소변의 색 비율',
                data: this.datas,
                datalabels: { anchor: 'center' },
                backgroundColor: this.colors,
                borderColor: this.colors,
                borderWidth: 1,
                pointStyle: 'circle'
            }]
        };

        const config = {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                        }
                    },
                    title: {
                        display: true,
                        text: 'Total - ' + total,
                        align: 'end',
                        font: { size: '18px' }
                    },
                    datalabels: {
                        font: {
                            size: '14px'
                        },
                        padding: 6,
                        formatter: (value) => {
                            const percentage = (value / total) * 100;
                            if (percentage < 3) return '';
                            return percentage.toFixed(1) + '%';
                        },
                    },
                },
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

        const ctx = document.getElementById('widget-pee').getContext('2d');
        let myChart = new Chart(ctx, config);

        await this.service.render();
    }
}