const express = require('express')
const swaggerJsdoc = require('swagger-jsdoc')
const swaggerUI = require('swagger-ui-express')
const app = express()
const port = process.env.PORT || 5000

/**
 * @swagger
 *  /temperature_up:
 *  post:
 *       description: Add an unit to the normal heating temperature   
 *       responses:
 *         '200':
 *                 description: Successful response
*/

/**
 * @swagger
 * /temperature_down:
 *  post:
 *        description: Substract an unit to the normal heating temperature             
 *        responses:
 *         '200':
 *                 description: Successful response
 */

/**
 *  @swagger
 *  /water_temperature_up:
 *  post:
 *        description: Add an unit to the normal water temperature         
 *        responses:
 *         '200':
 *                 description: Successful response
 */

/**
 * @swagger
 * /water_temperature_down:
 *  post:
 *        description: Add an unit to the normal water temperature        
 *        responses:
 *         '200':
 *                description: Successful response
 */

/**
 * @swagger
 * /statistics/temperature:
 *  post:
 *        description: returns an array which contains information about how much temeprature was consumed   
 *        responses:
 *         '200':
 *                description: Successful response
 */

/**
 * @swagger
 * /statistics/water_temperature:
 * post:
 *        description:  returns an array 
 *        responses:
 *         '200':
 *                description: Successful response
 */

const swaggerOptions = {
    swaggerDefinition: {
      info: {
        title: 'Heating system',
        description: 'It helps people to be always connected with their heating system.',
        contact: {
            name: 'The Four'
        },
        servers: ['http://localhost:5000']
      }
    },
    apis: ['generate_doc.js'], 
  };
  
const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use("/api-docs", swaggerUI.serve, swaggerUI.setup(swaggerDocs))


app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
})