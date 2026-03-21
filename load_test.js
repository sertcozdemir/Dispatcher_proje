import http from 'k6/http';
import { check, sleep} from 'k6';
export const options = {
    scenarios: {
        load_test: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                {duration: '20s', target:10},
                {duration: '20s', target:50},
                {duration: '20s', target:100},
                {duration: '20s', target:0},
            ],
        },
    },
    thresholds: {
        http_req_failed: ['rate<0.05'],
        http_req_duration: ['p(95)<1500'],
    }
};
const BASE_URL = 'http://host.docker.internal:8000';
const TOKEN = 'mysecrettoken';

export default function() {
    const params = {
        headers:{
            Authorization: `Bearer ${TOKEN}`,
        },
    };
    const userRes=http.get(`${BASE_URL}/users/2`, params);
    check(userRes, {
        'users status is 200': (r) => r.status===200,
        'users response has name': (r) => r.json('name') !==null,
    });
    const productRes = http.get(`${BASE_URL}/product/5`,params);
    check(productRes,{
        'products status is 200': (r) => r.status===200,
        'products response has name': (r) => r.json('name')!==null,
    });
    sleep(1);
}
