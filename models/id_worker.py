# gem-snowflake
# gem-snowflake is a variant of Python implementation inspired of Twitter's snowflake service
# Referrals:
# Twitter snowflake: https://github.com/twitter/snowflake

# 39 bits for time in units of 10 milliseconds
# 16 bits for a machine id
# 8 bits for a sequence number
import time


class IdWorker(object):
    def __init__(self, machine_id):
        self.machine_id = machine_id

        self.gemepoch = 1548084439

        self.sequence = 0
        self.sequence_bits = 8
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)
        self.machine_id_bits = 16
        self.max_machine_id = -1 ^ (-1 << self.machine_id_bits)

        self.sequence_shift = 0
        self.machine_id_shift = self.sequence_bits
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits

        self.last_timestamp = -1

        if self.machine_id > self.max_machine_id or self.machine_id < 0:
            raise Exception("machine id can't be greater than {} or less than zero".format(self.max_machine_id))

    def _generate_time(self):
        return int(time.time() * 1000)

    def _bit_extracted(self, number, k, p):
        return ((1 << k) - 1) & (number >> (p - 1))

    def _till_next_millis(self, last_timestamp):
        timestamp = self._generate_time()
        while timestamp <= last_timestamp:
            timestamp = self._generate_time()

        return timestamp

    def next_id(self):
        timestamp = self._generate_time()

        if self.last_timestamp > timestamp:
            raise Exception(
                'Clock moved backwards. Refusing to generate id for %i milliseconds'.format(self.last_timestamp))

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask

            if self.sequence == 0:
                timestamp = self._till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return (self._bit_extracted(timestamp - self.gemepoch, 39, 1) << self.timestamp_shift) | \
               (self._bit_extracted(self.machine_id, 16, 1) << self.machine_id_shift) | \
               (self._bit_extracted(self.sequence, 8, 1) << self.sequence_shift)
