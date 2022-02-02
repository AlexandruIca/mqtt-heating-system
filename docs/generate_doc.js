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
 * /temperature_usage:
 *  post:
 *        description: It makes the arithmetic mean of the temperatures recorded every day of the current month      
 *        responses:
 *         '200':
 *                description: Successful response
 */

/**
 * @swagger
 * /water_temperature_usage:
 *  post:
 *        description: It makes the arithmetic mean of the water temperatures recorded every day of the current month   
 *        responses:
 *         '200':
 *                description: Successful response
 */
 
/**
 * @swagger
 * /schedule_temp:
 *  post:
 *        description: It sets a certain temperature for a certain range 
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