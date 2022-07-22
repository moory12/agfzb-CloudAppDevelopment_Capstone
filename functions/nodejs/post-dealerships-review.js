/**
 * Get all dealerships matching state
 */

const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({apikey: params.IAM_API_KEY})
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbListPromise = createNewReview(cloudant, "reviews", params.REVIEW);
    return dbListPromise;
    return dbListPromise;
}


/*
Sample implementation to create a record in a db.
*/
function createNewReview(cloudant, dbname, review) {
    return new Promise((resolve, reject) => {
        cloudant.putDocument({db: dbname, review})
            .then((result) => {
                resolve({result: result.result.docs});
            })
            .catch(err => {
                console.log(err);
                reject({err: err});
            });

    })
}
