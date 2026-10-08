import json
import logging
import telnetlib3
import socket
import asyncio


class Dubbo:
    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, timeout=6000):
        self.host = host
        # self.port = port
        self.timeout = timeout
        self.reader = None
        self.writer = None

    async def connect(self):
        try:
            self.reader, self.writer = await telnetlib3.open_connection(self.host)
            await self.writer.drain()
        except (ConnectionRefusedError, TimeoutError, OSError) as e:
            logging.error(f"Failed to connect to {self.host}:{str(e)}")
            raise

    def close(self):
        if self.writer:
            self.writer.close()
            self.writer.wait_closed()

    async def command(self, flag, str_=""):
        try:
            data = await self.reader.read_until(flag.encode(), timeout=self.timeout)
            self.writer.write(str_.encode() + b"\n")
            await self.writer.drain()
            return data
        except (socket.timeout, ConnectionResetError, ConnectionAbortedError) as e:
            logging.error(f"Command execution failed: {str(e)}")
            raise

    async def invoke(self, service_name, method_name, arg):
        command_str = f"invoke {service_name}.{method_name}({json.dumps(arg)})"
        await self.command(Dubbo.prompt, command_str)
        data = await self.command(Dubbo.prompt, "")
        data = str(data, encoding='utf-8')
        dt = data.split("\r\n")[1]
        return json.loads(dt[8:])

    async def invoke_multi_param(self, service_name, method_name, *args):
        command_str = f"invoke {service_name}.{method_name}{args}"
        await self.command(Dubbo.prompt, command_str)
        data = await self.command(Dubbo.prompt, "")
        data = str(data, encoding='utf-8')
        dt = data.split("\r\n")[1]
        return json.loads(dt[8:])

    async def list_services(self):
        await self.command(Dubbo.prompt, "list")
        data = await self.command(Dubbo.prompt, "")
        data = str(data, encoding='utf-8')
        services = data.split("\r\n")[1:]
        return services


if __name__ == '__main__':
    async def run():
        dubbo_conn = Dubbo(host="106.15.234.139:22181")
        await dubbo_conn.connect()
        request = {
            'channelId': 'your_channel_id',
            'channelUid': 'your_channel_uid',
            'mobileNo': 'your_mobile_no',
            'partnerUserNo': 'your_partner_user_no',
            'registerScene': 'your_register_scene'
        }

        response = await dubbo_conn.invoke('io.kyoto.pillar.cis.user.UserInfoFacadeImpl', 'getOrAddUserByHub', request)
        print(f"dubbo_conn.invoke::response::response::{response}")

        dubbo_conn.close()

    asyncio.run(run())