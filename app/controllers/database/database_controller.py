import boto3
import time

# TODO: Recreate table object after a few hours
class DynamoDBController:
    def __init__(self, table_name, primary_key):
        """
        Simple controller to interact with AWS DynamoDB.

        Args:
            table_name: The name of the table
            primary_key: The primary key associated with this table.
        """
        self.table_name = table_name
        self.session_created_at = time.time()
        self.primary_key = primary_key
        self.table = boto3.resource("dynamodb").Table(self.table_name)

    def _refresh_session(self):
        self.table = boto3.resource("dynamodb").Table(self.table_name)

    def _check_session(self):
        pass
        # TODO

    def put(self, primary_key_value: str, data: dict):
        """
        Inserts a new entry to the DynamoDB table.
        Primary keys are idempotent: Inserting a value with an existing key updates the entry.

        Args:
            primary_key_value: The primary key used on the DynamoDB table
            data: The data to be stored with this item

        Returns:

        """
        response = self.table.put_item(
            Item={
                self.primary_key: primary_key_value,
                "data": data
            }
        )
        return response

    def delete(self, primary_key_value: str):
        """
        Deletes an entry in the table given a primary_key_value.
        Args:
            primary_key_value: The primary key of the entry that is to be deleted.

        Returns:

        """
        response = self.table.delete_item(
            Key={
                self.primary_key: primary_key_value
            }
        )
        return response

    def get_item(self, primary_key_value: str) -> dict:
        """
        Gets an entry in the DynamoDB table given a value of the primary key.
        Args:
            primary_key_value: The value of the primary key which corresponds to the entry that is to be fetched

        Returns: The entry as a dictionary

        """
        response = self.table.get_item(
            Key={
                self.primary_key: primary_key_value
            }
        )
        return response["Item"]

    def scan_table(self) -> dict:
        """
        Scans the table and returns all entries.

        Returns: All entries in the table as a dict.

        TODO: Check pageination or remove

        """
        response = self.table.scan()
        return response['Items']


if __name__ == "__main__":
    myController = DynamoDBController("TestTable", "item_id")
    print(myController.scan_table())
    import time
    time.sleep(3*60*60+100)
    print(myController.scan_table())
    myController.put("abcdefg", {"hello": "from_local"})


