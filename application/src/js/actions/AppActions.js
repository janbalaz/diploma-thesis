var AppDispatcher = require('../dispatcher/AppDispatcher');
var AppConstants = require('../constants/AppConstants');

var AppActions = {
    addItem: function(item){
        AppDispatcher.dispatch({
            actionType:AppConstants.ADD_ITEM,
            item: item
        })
    },

    loadCharts: function(){
        AppDispatcher.dispatch({
            actionType:AppConstants.LOAD_CHARTS
        })
    }
};

module.exports = AppActions;
