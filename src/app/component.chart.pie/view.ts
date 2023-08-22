import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    @Input() title: any;
    @Input() labels: any;
    @Input() datas: any;
    @Input() colors: any;

    constructor(
        public service: Service
    ) { }

    public async ngOnInit() {
        await this.service.init();
        const data = {
            labels: this.labels,
            datasets: [{
                label: '건수별 / 연도별',
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

        const ctx = document.getElementById('widget-pie').getContext('2d');
        let myChart = new Chart(ctx, config);
        await this.service.render();
    }
}