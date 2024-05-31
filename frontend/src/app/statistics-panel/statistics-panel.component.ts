import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { TabsModule } from 'ngx-bootstrap/tabs';
import Chart from 'chart.js/auto';

type TopTagData = {
	tag: string,
	count: number,
}

@Component({
	selector: 'app-statistics-panel',
	standalone: true,
	imports: [TabsModule],
	templateUrl: './statistics-panel.component.html',
	styleUrl: './statistics-panel.component.css'
})
export class StatisticsPanelComponent implements AfterViewInit{

	@ViewChild('myCanvas') canvas!: ElementRef<HTMLCanvasElement>;
	chart!: Chart;

	topTagsArray: TopTagData[] = [];

	constructor() {}

	ngAfterViewInit(): void {
		this.createChart();
	}

	createChart() {
		this.chart = new Chart(this.canvas.nativeElement, {
		  type: 'bar', // or 'bar', 'pie', etc.
		  data: {
			labels: ['January', 'February', 'March', 'April', 'May', 'June'],
			datasets: [
			  {
				label: 'Top 10 tagów',
				data: [12, 19, 3, 5, 2, 3],
				backgroundColor: 'rgba(54, 162, 235, 0.2)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 1
			  }
			]
		  },
		  options: {
			maintainAspectRatio: false
		  }
		});
	  }

}
