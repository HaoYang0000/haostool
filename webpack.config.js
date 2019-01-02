const webpack = require('webpack');
const config = {
    entry:  __dirname + '/app/frontend/js/index.jsx',
    output: {
        path: __dirname + '/app/frontend/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
	  rules: [
		  {
		   test: /\.jsx?/,
		   loader: 'babel-loader',
		   exclude: /node_modules/,
		  query:{
		     presets: ['react','es2015']
		   }
		}
	  ]
	}
};
module.exports = config;