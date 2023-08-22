import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    // @Input() title: any;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        const data = {
            labels: ['CHART 1', 'CHART 2', 'CHART 3', 'CHART 4'],
            datasets: [{
                label: '건수별 / 연도별',
                data: [80, 40, 50, 50],
                backgroundColor: [
                    '#5041F2',
                    '#F2748D',
                    '#9996B7',
                    '#DFDEF7'
                ],
                borderColor: [
                    '#5041F2',
                    '#F2748D',
                    '#9996B7',
                    '#DFDEF7'
                ],
                borderWidth: 1,
                pointStyle: 'circle'
            }]
        };

        const config = {
            type: 'doughnut',
            data: data,
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        // display:false,
                        position: 'right',
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

        const ctx = document.getElementById('widget-doughnut').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}
