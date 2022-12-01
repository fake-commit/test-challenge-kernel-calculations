# Exchange rates API

* [How to start](#how-to-start)
* [API Request & Response Examples](#request--response-examples)

## How to start

To run the project, clone the repository, navigate to the root of the repository, and simply run the command:

    $ docker-compose up

## Environment variables

For the convenience, I added .env file with the database credentials to the repository.


## API Request & Response Examples

### API Resources

  - [Get list of calculations](#get-list-of-calculations-results)
  - [Get calculation results by id](#get-calculation-result-by-id)
  - [Start new calculation](#run-calculation)

##  Get list of calculations

### GET /api/kernel/calculations/

| Parameter  | Type     | Description                                                                 |
|:-----------|:---------|:----------------------------------------------------------------------------|
| `page`     | `int`    | **Optional**. Page number, results are paginated by 10 items on a page.     |
| `ordering` | `string` | **Optional**. Ordering (available options: `-date_started`, `date_started`) |


####  Response body:

```
{
    "count": int,
    "next": url,
    "previous": url,
    "results": [
        {
            "task_id": uuid,
            "status": str,
            "date_created": datetime,
            "date_done": datetime
        },
        ...
    ]
}
```

## Get calculation results by id

```http
GET /api/kernel/calculations/{task_id}/
```

| Parameter | Type    | Description                                                                        |
| :--- |:--------|:-----------------------------------------------------------------------------------|
| `task-id` | `uuid`  | **Required**. Caclucation task id                                                  |
| `fields` | `array` | **Optional**.  Optional fields in response (available options: `calculation_time`) |

####  Response body:

```
{
    "task_id": uuid,
    "status": str,
    "result": [
        {
            "date": datetime,
            "liquid": float,
            "oil": float,
            "water": float,
            "wct": float
        },
        ...
    ],
    "calculation_time": "float"
}
```

## Start new calculation

```http
### POST /api/kernel/calculate/
```

####  Request body:

```
{
    "date_start": date,
    "date_fin": date,
    "lag": int
}
```

####  Response body:

```
{
    "task_id": uuid
}
```
