import asyncio
import io
import aiohttp
import aiofiles
import requests
import csv
import datetime
import logging
import sys
import argparse


def ex1():
    response = requests.get('https://reqres.in/api/users')
    if response.status_code // 100 == 2:
        users = response.json()['data']
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f'User ID: {user['id']}\n')
                f.write(f'Name: {user['first_name']} {user["last_name"]}\n')
                f.write(f'Email: {user['email']}\n')
                f.write(f'Avatar: {user["avatar"]}\n\n')
        print("File created successfully")


def ex2():
    num_of_users = int(input('How many users do you want to generate? '))
    response = requests.get(f'https://randomuser.me/api/?results={num_of_users}')
    if response.status_code // 100 == 2:
        users = response.json()['results']
        contents = [['first name', 'last name', 'email', 'gender', 'country', 'age']]
        for user in users:
            user_data = [user['name']['first'], user['name']['last'], user['email'], user['gender'],
                         user['location']['country'], user['dob']['age']]
            contents.append(user_data)
        with open('users.csv', 'w', encoding='UTF-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(contents)


def ex3():
    response = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population')
    if response.status_code // 100 == 2:
        data = response.json()['data']
        contents = [['year', 'population', 'population change (%)']]
        data_simplified = []
        for entry in data:
            data_simplified.append([entry['ID Year'], entry['Population']])
        for i in range(len(data_simplified) - 1):
            pop_change = data_simplified[i][1] - data_simplified[i + 1][1]
            data_simplified[i].append(pop_change / data_simplified[i + 1][1] * 100)
        data_simplified[-1].append('--')
        contents.extend(data_simplified)
        with open('population.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(contents)
        with open('population.txt', 'w') as f:
            f.write(f'Earliest year: {data_simplified[-1][0]}, population: {data_simplified[-1][1]}\n')
            f.write(f'Latest year: {data_simplified[0][0]}, population: {data_simplified[0][1]}\n')
            pop_change = data_simplified[0][1] - data_simplified[-1][1]
            f.write(f'Total population change (%): {pop_change / data_simplified[-1][1] * 100}')


def get_request(url: str, log: io.TextIOWrapper) -> requests.Response:
    response = requests.get(url)
    if response.status_code // 100 == 2:
        log.write(f"{datetime.datetime.now()} - {url} - {response.status_code} Success\n")
        return response
    elif response.status_code // 100 == 5:
        print(f"{url} - Server error, try again later")
    elif response.status_code == 404:
        print(f"{url} - Page not found")
    elif response.status_code == 403:
        print(f"{url} - Access denied")
    else:
        print(f"{url} - Error, try again later")
    log.write(f"{datetime.datetime.now()} - {url} - {response.status_code} Failure\n")
    return response


def write_to_file_formatted(data: str, filename: str) -> None:
    with open(filename, 'w', encoding='UTF-8') as f:
        indent = 0
        for char in data:
            if char in '}]':
                indent -= 1
                f.write('\n' + '\t' * indent)
            f.write(char)
            if char in '{[,':
                if char in '[{':
                    indent += 1
                f.write('\n' + '\t' * indent)


def challenge1():
    with open('log.txt', 'a+') as log:
        log.write(f"{datetime.datetime.now()} - Accessing https://reqres.in/api/users\n")
        response = get_request("https://reqres.in/api/users", log)
        write_to_file_formatted(response.text, 'challenge_reqres.txt')
        users = response.json()['data']
        contents = [['total users'], [len(users)], ['id', 'email', 'first name', 'last name', 'avatar']]
        for i in [0, -1]:
            contents.append([users[i]['id'], users[i]['email'], users[i]['first_name'], users[i]['last_name'],
                             users[i]['avatar']])
        contents.append([])

        log.write(f"{datetime.datetime.now()} - Accessing https://randomuser.me/api/?results=5\n")
        response = get_request("https://randomuser.me/api/?results=5", log)
        write_to_file_formatted(response.text, 'challenge_randomuser.txt')
        contents.append(['nationality', 'male', 'female'])
        genders = {}
        for user in response.json()['results']:
            if user['nat'] not in genders:
                genders[user['nat']] = [0, 0]
            if user['gender'] == 'male':
                genders[user['nat']][0] += 1
            else:
                genders[user['nat']][1] += 1
        for nationality in genders:
            contents.append([nationality, genders[nationality][0], genders[nationality][1]])
        contents.append([])

        log.write(
            f"{datetime.datetime.now()} - Accessing https://datausa.io/api/data?drilldowns=Nation&measures=Population\n")
        response = get_request("https://datausa.io/api/data?drilldowns=Nation&measures=Population", log)
        write_to_file_formatted(response.text, 'challenge_datausa.txt')
        contents.append(['year', 'population'])
        data = response.json()['data'][0]
        contents.append([data['ID Year'], data['Population']])

        with open('summary.csv', 'w', encoding='UTF-8', newline='') as summary:
            writer = csv.writer(summary)
            writer.writerows(contents)


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("challenge_log")
logging.getLogger("chardet.charsetprober").disabled = True


async def write_user_to_files(user: dict, nationality: str) -> None:
    logger.info("Writing user %s to file 'master.csv'")
    user_row = [user['name'], user['gender'], user['age'], user['email']]
    logger.info("Writing user %s to file 'master.csv'", user['name'])
    async with aiofiles.open('master.csv', 'a+', encoding='UTF-8') as f:
        await f.write(','.join([nationality.upper()] + user_row) + '\n')
        logger.info("Finished writing user %s", user['name'])
    logger.info("Writing user %s to file '%s'", user['name'], f'users_{nationality}.csv')
    async with aiofiles.open(f'users_{nationality}.csv', 'a+', encoding='UTF-8') as f:
        await f.write(','.join(user_row) + '\n')
        logger.info("Finished writing user %s", user['name'])


async def get_users_of_nationality(nationality: str, session: aiohttp.ClientSession, raw_data: bool):
    logger.info("Sending GET request to %s", f'https://randomuser.me/api/?results=20&nat={nationality}')
    async with session.get(f'https://randomuser.me/api/?results=20&nat={nationality}') as response:
        response.raise_for_status()
        logger.info("Got response [%s] for URL: %s", response.status,
                    f'https://randomuser.me/api/?results=20&nat={nationality}')
        if raw_data:
            async with aiofiles.open(f'users_{nationality}.json', 'w', encoding='utf-8') as f:
                raw_json = await response.text()
                await f.write(raw_json)
        data = await response.json()
        for user in data['results']:
            yield user


async def write_nation_to_files(nation: str, session: aiohttp.ClientSession, raw_data: bool) -> None:
    try:
        users = get_users_of_nationality(nation, session, raw_data)
        async for user in users:
            user_trimmed = {
                'name': f'{user['name']['first']} {user['name']['last']}',
                'gender': user['gender'],
                'age': str(user['dob']['age']),
                'email': user['email'],
            }
            await write_user_to_files(user_trimmed, nation)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            f'https://randomuser.me/api/?results=20&nat={nation}',
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return None
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occurred:  %s", getattr(e, "__dict__", {})
        )
        return None


def count_genders(data: list) -> tuple:
    male, female = 0, 0
    for user in data:
        for key, value in user.items():
            if key == 'gender':
                if value == 'male':
                    male += 1
                else:
                    female += 1
    return male, female


def get_age_statistics(data: list) -> tuple:
    min_age, max_age, average = float('inf'), -float('inf'), 0
    for user in data:
        for key, value in user.items():
            if key == 'age':
                value = int(value)
                average += value
                min_age = min(min_age, value)
                max_age = max(max_age, value)
    return min_age, max_age, average / len(data)


def count_domains(data: list) -> dict:
    domain_counts = {}
    for user in data:
        for key, value in user.items():
            if key == 'email':
                domain = value.split('@')[1]
                if domain in domain_counts:
                    domain_counts[domain] += 1
                else:
                    domain_counts[domain] = 1
    return domain_counts


async def challenge2(nations: list, raw_data: bool = False):
    with open('master.csv', 'w', newline='') as master:
        csv.writer(master).writerow(['nationality', 'name', 'gender', 'age', 'email'])
    async with aiohttp.ClientSession() as session:
        tasks = []
        for nation in nations:
            with open(f'users_{nation}.csv', 'w', newline='') as f:
                csv.writer(f).writerow(['name', 'gender', 'age', 'email'])
            tasks.append(write_nation_to_files(nation=nation, session=session, raw_data=raw_data))
        await asyncio.gather(*tasks)
    nations_data = {}
    for nation in nations:
        nations_data[nation] = []
        with open(f'users_{nation}.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nations_data[nation].append(row)
    with open('comparison.txt', 'w', encoding='utf-8') as f:
        f.write("Gender Distribution\nNationality\tMale\tFemale\n")
        lines = []
        for nation in nations_data.keys():
            male, female = count_genders(nations_data[nation])
            lines.append(f'{nation.upper()}\t{male}\t{female}\n')
        f.writelines(lines)

        f.write('\nAge Statistics\nNationality\tMin\tMax\tAverage\n')
        lines = []
        for nation in nations_data.keys():
            min_age, max_age, average = get_age_statistics(nations_data[nation])
            lines.append(f'{nation.upper()}\t{min_age}\t{max_age}\t{average}\n')
        f.writelines(lines)

        f.write('\nEmail Domain Frequency\nNationality\tDomain\tCount\n')
        lines = []
        for nation in nations_data.keys():
            domain_counts = count_domains(nations_data[nation])
            for domain in domain_counts:
                lines.append(f'{nation.upper()}\t{domain}\t{domain_counts[domain]}\n')
        f.writelines(lines)


if __name__ == "__main__":
    raw = False
    parser = argparse.ArgumentParser(
        prog='C:\\Users\\User\\PycharmProjects\\DevSecOps\\rest-api-lab.py',
        description='Aggregate user information from randomuser.me'
    )
    parser.add_argument('-r', '--Raw', action='store_true', dest='raw')
    parser.add_argument('-n', '--Nationalities', nargs='+', dest='nationalities')
    arguments = parser.parse_args(sys.argv[1:])
    all_nationalities = ['au', 'br', 'ca', 'ch', 'de', 'dk', 'es', 'fi', 'fr', 'gb', 'ie', 'in', 'ir', 'mx',
                         'nl', 'no', 'nz', 'rs', 'tr', 'ua', 'us']
    nationalities = all_nationalities if arguments.nationalities is None else arguments.nationalities
    asyncio.run(challenge2(nations=nationalities, raw_data=arguments.raw))
