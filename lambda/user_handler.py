import json
import boto3
import uuid
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
ses = boto3.client('ses')

def lambda_handler(event, context):
    """
    Main Lambda handler for user operations
    """
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Route to appropriate handler
        if path == '/lambda/users' and http_method == 'GET':
            return get_users(event, context)
        elif path == '/lambda/users' and http_method == 'POST':
            return create_user(event, context)
        elif path.startswith('/lambda/users/') and http_method == 'GET':
            user_id = path.split('/')[-1]
            return get_user(user_id, event, context)
        elif path == '/lambda/process' and http_method == 'POST':
            return process_data(event, context)
        elif path == '/lambda/analytics' and http_method == 'GET':
            return get_analytics(event, context)
        else:
            return {
                'statusCode': 404,
                'headers': get_cors_headers(),
                'body': json.dumps({
                    'error': 'Route not found',
                    'path': path,
                    'method': http_method
                })
            }
            
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

def get_users(event, context):
    """Get all users from DynamoDB"""
    try:
        table = dynamodb.Table('demo-users')
        response = table.scan()
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'success': True,
                'data': response['Items'],
                'count': response['Count']
            }, default=str)
        }
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Failed to get users',
                'message': str(e)
            })
        }

def create_user(event, context):
    """Create a new user in DynamoDB"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        if not body.get('name') or not body.get('email'):
            return {
                'statusCode': 400,
                'headers': get_cors_headers(),
                'body': json.dumps({
                    'error': 'Name and email are required'
                })
            }
        
        # Create user object
        user = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'email': body['email'],
            'createdAt': datetime.utcnow().isoformat(),
            'updatedAt': datetime.utcnow().isoformat(),
            'source': 'lambda'
        }
        
        # Save to DynamoDB
        table = dynamodb.Table('demo-users')
        table.put_item(Item=user)
        
        # Send welcome email (optional)
        try:
            send_welcome_email(user['email'], user['name'])
        except Exception as email_error:
            logger.warning(f"Failed to send welcome email: {str(email_error)}")
        
        return {
            'statusCode': 201,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'success': True,
                'data': user,
                'message': 'User created successfully'
            }, default=str)
        }
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Failed to create user',
                'message': str(e)
            })
        }

def get_user(user_id, event, context):
    """Get a specific user by ID"""
    try:
        table = dynamodb.Table('demo-users')
        response = table.get_item(Key={'id': user_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': get_cors_headers(),
                'body': json.dumps({
                    'error': 'User not found'
                })
            }
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'success': True,
                'data': response['Item']
            }, default=str)
        }
        
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Failed to get user',
                'message': str(e)
            })
        }

def process_data(event, context):
    """Process data and store results in S3"""
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Process the data (example: transform and analyze)
        processed_data = {
            'id': str(uuid.uuid4()),
            'originalData': body,
            'processedAt': datetime.utcnow().isoformat(),
            'processingResults': {
                'status': 'completed',
                'recordsProcessed': len(body.get('records', [])),
                'summary': 'Data processed successfully'
            }
        }
        
        # Store results in S3
        s3_key = f"processed-data/{processed_data['id']}.json"
        s3.put_object(
            Bucket='demo-processed-data',
            Key=s3_key,
            Body=json.dumps(processed_data, default=str),
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'success': True,
                'data': processed_data,
                's3Location': f"s3://demo-processed-data/{s3_key}"
            }, default=str)
        }
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Failed to process data',
                'message': str(e)
            })
        }

def get_analytics(event, context):
    """Get analytics data"""
    try:
        # Get user count from DynamoDB
        table = dynamodb.Table('demo-users')
        user_response = table.scan(Select='COUNT')
        
        # Get file count from S3
        try:
            s3_response = s3.list_objects_v2(Bucket='demo-storage')
            file_count = s3_response.get('KeyCount', 0)
        except:
            file_count = 0
        
        analytics = {
            'totalUsers': user_response['Count'],
            'totalFiles': file_count,
            'lambdaInvocations': context.get_remaining_time_in_millis(),
            'timestamp': datetime.utcnow().isoformat(),
            'region': context.invoked_function_arn.split(':')[3],
            'functionName': context.function_name
        }
        
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'success': True,
                'data': analytics
            }, default=str)
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({
                'error': 'Failed to get analytics',
                'message': str(e)
            })
        }

def send_welcome_email(email, name):
    """Send welcome email using SES"""
    try:
        ses.send_email(
            Source='noreply@demo-app.com',
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'Welcome to AWS Demo App!'},
                'Body': {
                    'Text': {
                        'Data': f'Hello {name},\n\nWelcome to our AWS Demo Application!\n\nBest regards,\nThe Demo Team'
                    },
                    'Html': {
                        'Data': f'''
                        <html>
                        <body>
                            <h2>Welcome to AWS Demo App!</h2>
                            <p>Hello {name},</p>
                            <p>Welcome to our AWS Demo Application!</p>
                            <p>You can now explore all the features including:</p>
                            <ul>
                                <li>File uploads to S3</li>
                                <li>Data processing with Lambda</li>
                                <li>Secure authentication with Cognito</li>
                                <li>Scalable backend with ECS</li>
                            </ul>
                            <p>Best regards,<br>The Demo Team</p>
                        </body>
                        </html>
                        '''
                    }
                }
            }
        )
        logger.info(f"Welcome email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        raise

def get_cors_headers():
    """Return CORS headers"""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
