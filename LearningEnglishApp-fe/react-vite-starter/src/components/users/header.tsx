import React, { useState } from 'react';
import { HomeOutlined, UserOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';
import { Menu } from 'antd';

const items: MenuProps['items'] = [
    {
        label: 'Home',
        key: 'home',
        icon: <HomeOutlined />,
    },
    {
        label: 'Account',
        key: 'account',
        icon: <UserOutlined />,
    },
];

const Header: React.FC = () => {
    const [current, setCurrent] = useState('home');

    const onClick: MenuProps['onClick'] = (e) => {
        setCurrent(e.key);
    };

    return (
        <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
    );
};

export default Header;
