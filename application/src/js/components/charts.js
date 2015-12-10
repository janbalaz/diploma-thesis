var React = require('react');
var AppStore = require('../stores/AppStore');
var Chart = require('react-google-charts').Chart;
var ChartStore = require('../stores/ChartStore');

function getChartState() {
  return {
    singleChart: ChartStore.get()
  };
}

var Charts = React.createClass({
    getInitialState: function() {
        return getChartState();
    },
    componentDidMount: function() {
        ChartStore.addChangeListener(this._onChange);
    },
    componentWillUnmount: function() {
        ChartStore.removeChangeListener(this._onChange);
    },
    addChangeListener: function(callback) {
        this.on(CHANGE_EVENT, callback);
    },
    removeChangeListener: function(callback) {
        this.removeListener(CHANGE_EVENT, callback);
    },
	render: function() {
		return (
			<div className="chart">
				<Chart chartType={this.props.chartType}
					   width={this.props.width}
					   height={this.props.height}
					   data={this.state.singleChart.dataArray}
					   options = {this.state.singleChart.options}
					   graph_id={this.props.chartType} />
			</div>
		);
	},
    _onChange: function() {
        this.setState(getChartState());
    }
});

module.exports = Charts;