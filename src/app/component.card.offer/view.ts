import { OnInit, Input } from '@angular/core';

export class Component implements OnInit {
    @Input() title: any;
    @Input() text: any;

    public async ngOnInit() {
    }
}