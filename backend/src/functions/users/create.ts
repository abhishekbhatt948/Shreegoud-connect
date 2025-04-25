import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';
import { v4 as uuidv4 } from 'uuid';
import * as yup from 'yup';
import middy from '@middy/core';
import httpJsonBodyParser from '@middy/http-json-body-parser';
import httpErrorHandler from '@middy/http-error-handler';
import httpCors from '@middy/http-cors';

const dynamoDb = DynamoDBDocumentClient.from(new DynamoDBClient({}));

const userSchema = yup.object().shape({
  name: yup.string().required(),
  email: yup.string().email().required(),
  phone: yup.string().required(),
  location: yup.string().required(),
  profession: yup.string().required(),
  department: yup.string(),
  expertise: yup.array().of(yup.string()),
});

const createUser = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  try {
    const userData = await userSchema.validate(event.body);

    const user = {
      id: uuidv4(),
      ...userData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    await dynamoDb.send(
      new PutCommand({
        TableName: `${process.env.STAGE}-users`,
        Item: user,
      })
    );

    return {
      statusCode: 201,
      body: JSON.stringify(user),
    };
  } catch (error) {
    console.error('Error creating user:', error);
    return {
      statusCode: error.name === 'ValidationError' ? 400 : 500,
      body: JSON.stringify({
        message: error.message,
      }),
    };
  }
};

export const handler = middy(createUser)
  .use(httpJsonBodyParser())
  .use(httpErrorHandler())
  .use(httpCors()); 