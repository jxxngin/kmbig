import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';
import { Chart } from 'chart.js/auto';

export class Component implements OnInit {
    // @Input() title: any;

    constructor(
        public service: Service,
    ) { }

    public async ngOnInit() {
        await this.service.init();
        const data = {
            labels: ['1-A', '1-B', '2-A', '2-B', '3-A', '3-B', '4-A', '4-B'],
            datasets: [
                {
                    backgroundColor: ['#AAA', '#777'],
                    data: [21, 79]
                },
                {
                    backgroundColor: ['#5041F2', '#5041F2'],
                    data: [33, 67]
                },
                {
                    backgroundColor: ['#F2748D', '#F2748D'],
                    data: [20, 80]
                },
                {
                    backgroundColor: ['#9996B7', '#9996B7'],
                    data: [10, 90]
                }
            ]
        };

        const config = {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {}
                    },
                }
            }
            
        };

        await this.service.render();
    }
}