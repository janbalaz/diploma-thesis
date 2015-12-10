var AppDispatcher = require('../dispatcher/AppDispatcher');
var EventEmitter = require('events').EventEmitter;
var AppConstants = require('../constants/AppConstants');
var assign = require('object-assign');

var CHANGE_EVENT = 'change';

var AppStore = assign({}, EventEmitter.prototype, {
  emitChange: function() {
    this.emit(CHANGE_EVENT);
  }
});

AppDispatcher.register(function(action) {

    switch(action.actionType) {
        case AppConstants.ADD_ITEM:
            console.log(action);
            AppStore.emitChange();
            break;

        case AppConstants.LOAD_CHARTS:
            AppStore.emitChange();
            break;
        default:
            // no op
  }
});

module.exports = AppStore;
