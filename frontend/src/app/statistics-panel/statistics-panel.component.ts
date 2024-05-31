import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { TabsModule } from 'ngx-bootstrap/tabs';
import Chart from 'chart.js/auto';
import { ServerService } from '../services/server.service';

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
export class StatisticsPanelComponent implements AfterViewInit {

	@ViewChild('myCanvas') canvas!: ElementRef<HTMLCanvasElement>;
	chart!: Chart;

	topTagsArray: TopTagData[] = [];

	constructor(private serverService: ServerService) { }

	ngAfterViewInit(): void {
		this.createTopTagsChart();
	}

	createTopTagsChart() {
		this.serverService.getTopTags(10).subscribe({
			next: (response: any) => {
				let labels = response.map((tag: any) => tag.tag);
				let data = response.map((tag: any) => tag.count);
				this.createChart(labels, data);
			},
			error: (error: Error) => {
				console.log(error);
			}
		})
	}

	createChart(labels: string[], data: number[]) {

		this.chart = new Chart(this.canvas.nativeElement, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'Top 10 tagów',
						data: data,
						backgroundColor: 'rgba(46, 204, 113, 0.2)',
						borderColor: 'rgba(46, 204, 113, 1)',
						borderWidth: 2,
					}
				]
			},
			options: {
				maintainAspectRatio: false,
				scales: {
					x: {
						ticks: {
							font: {
								size: 16
							}
						},
					},
					y: {
						ticks: {
							font: {
								size: 16
							}
						}
					}
				},
				plugins: {
					legend: {
						labels: {
							font: {
								size: 20
							}
						}
					}
				}
			}
		});
	}

}
