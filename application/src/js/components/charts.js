var React = require('react');
var AppStore = require('../stores/AppStore');
var Chart = require('react-google-charts').Chart;

var BarChartData =  {
     dataArray : [
         ['Element', 'Density', { role: 'style' }],
         ['Copper', 8.94, '#b87333'],            // RGB value
         ['Silver', 10.49, 'silver'],            // English color name
         ['Gold', 19.30, 'gold'],
         ['Platinum', 21.45, 'color: #e5e4e2' ] // CSS-style declaration
      ],
      options : {
        title: "Density of Precious Metals, in g/cm^3",
        width: 600,
        height: 400,
        bar: {groupWidth: "95%"},
        legend: { position: "none" }
      }
};
/*
<Chart chartType={this.props.chartType}
					   width={this.props.width}
					   height={this.props.height}
					   data={this.props.chartState.singleChart.dataArray}
					   options = {this.props.chartState.singleChart.options}
					   graph_id={this.props.chartType} />
 */

var Charts = React.createClass({
    getInitialState: function() {
		return {
			BarChart: {
				data: [],
				chartType: "",
				options : {}
			}
		};
	},
	componentDidMount: function() {
		var BarChart = {
			data : BarChartData.dataArray,
			options: BarChartData.options,
			chartType: "BarChart",
			div_id: "BarChart"
		};
		this.setState({
			'BarChart': BarChart
		});
	},
	render: function() {
		return (
			<div className="Examples">
				<h3> Bar Chart </h3>
				<Chart chartType={this.state.BarChart.chartType}
                       width={"500px"}
                       height={"300px"}
                       data={this.state.BarChart.data}
                       options = {this.state.BarChart.options}
                       graph_id={this.state.BarChart.div_id} />
			</div>
		);
	}
});

module.exports = Charts;