import { OnInit, Input } from '@angular/core';

export class Component implements OnInit {
    @Input() title: any;
    @Input() num: any;
    @Input() unit: any;

    public async ngOnInit() {
    }
}