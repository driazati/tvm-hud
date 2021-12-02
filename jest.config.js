const fs = require("fs");

let config = {
  moduleNameMapper: {
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$":
      "<rootDir>/__mocks__/fileMock.js",
    "\\.(css|less)$": "identity-obj-proxy",
  },
  setupFiles: ["jest-canvas-mock"],
};

let node_modules = fs.readdirSync("node_modules").join("|");
config.transformIgnorePatterns = [`/node_modules/(?!${node_modules})`];

module.exports = config;
