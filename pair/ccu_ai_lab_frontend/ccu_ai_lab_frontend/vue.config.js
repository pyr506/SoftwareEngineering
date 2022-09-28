module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? './'
    : './',
  outputDir: 'center',
  assetsDir: './center/assets/',
}

