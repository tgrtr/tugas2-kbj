from kombu import Exchange, Queue

broker_url = 'amqp://guest:guest@localhost:5672//'
result_backend = 'rpc://'

fanout_exchange = Exchange('ex_fanout', type='fanout')
topic_exchange = Exchange('ex_topic', type='topic')

task_queues = (
    Queue('q_fanout_1', fanout_exchange),
    Queue('q_fanout_2', fanout_exchange),
    Queue('q_topic_spesifik', topic_exchange, routing_key='sensor.suhu.ruang1'),
    Queue('q_wildcard_bintang', topic_exchange, routing_key='sensor.suhu.*'),
    Queue('q_wildcard_pagar', topic_exchange, routing_key='sensor.#'),
)
