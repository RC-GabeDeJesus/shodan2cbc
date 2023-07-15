import shodan
import pandas as pd
import subprocess

def query_shodan(api_key, hashes):
    api = shodan.Shodan(api_key)
    results = []

    for hash_ in hashes:
        try:
            result = api.search(f'ssl.cert.serial:{hash_}')
            results.extend(result['matches'])
        except shodan.APIError as e:
            print(f'Error: {e}')

    return results

def generate_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def main():
    api_key = 'SHODAN_API_KEY'
    ssl_hashes = ['146473198']  # replace with your hashes
    filename = 'shodan_results.csv'
    
    results = query_shodan(api_key, ssl_hashes)
    generate_csv(results, filename)
    run_parser()


def run_parser():
    output = subprocess.check_output(['python3', 'parse_infra.py'])
    print(output.decode())

if __name__ == '__main__':
    main()
