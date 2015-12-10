/** @jsx React.DOM */
var React = require('react');
var AppActions = require('../actions/AppActions');
var AppStore = require('../stores/AppStore');
var ChartStore = require('../stores/ChartStore');
var Charts = require('./charts.js');

/*
<Charts width="600" height="600" chartType="BarChart" chartState={this.state.chartState} />
 */

function getChartState() {
  return {
    singleChart: ChartStore.get()
  };
}

var App = React.createClass({
    getInitialState: function() {
        return {
            chartState: getChartState()
        };
    },
    handleClick:function(){
        AppActions.addItem('this is the item');
    },
    componentDidMount: function() {
        AppActions.loadCharts();
        ChartStore.addChangeListener(this._onChange);
    },
    componentWillUnmount: function() {
        ChartStore.removeChangeListener(this._onChange);
    },
    render:function(){
        return (
            <div className="row">
                <div className="row">
                    <div className="col-md-6">
                        <h3 onClick={this.handleClick}>Click this Title, then check console</h3>
                    </div>
                    <div className="col-md-6">
                        TODO post formular
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-6">
                        OMG
                        <Charts />
                    </div>
                </div>
            </div>
        )
    },
    _onChange: function() {
        this.setState({
            chartState: getChartState()
        });
    }
  });

module.exports = App;
