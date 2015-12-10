/** @jsx React.DOM */
var React = require('react');
var AppActions = require('../actions/AppActions');
var AppStore = require('../stores/AppStore');
var ChartStore = require('../stores/ChartStore');
var Charts = require('./charts.js');

var App = React.createClass({
    handleClick:function(){
        AppActions.addItem('this is the item');
    },
    componentDidMount: function() {
        AppActions.loadCharts();
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
                        <Charts width="600" height="600" chartType="BarChart" />
                    </div>
                </div>
            </div>
        )
    }
  });

module.exports = App;
